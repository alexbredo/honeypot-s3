#!/usr/bin/env python

# Copyright (c) 2014 Alexander Bredo
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the 
# following conditions are met:
# 
# 1. Redistributions of source code must retain the above 
# copyright notice, this list of conditions and the following 
# disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above 
# copyright notice, this list of conditions and the following 
# disclaimer in the documentation and/or other materials 
# provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

import os
import os.path
import shutil
import datetime
import hashlib
from tornado import ioloop, httpserver, web, autoreload
from aws.AWSError import *
from aws.AWSAuth import *

class S3Server(web.Application):
	def __init__(self, root_directory):
		self.directory = os.path.abspath(root_directory)
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)
		web.Application.__init__(self, [
			(r"/", RootHandler),
			(r"/(favicon\.ico)", web.StaticFileHandler, {'path': './static/'}),
			(r"/([^/]+)/?", BucketHandler),
			(r"/([^/]+)/(.+)", ObjectHandler),
		], debug=True)


class BaseHandler(web.RequestHandler):
	#def initialize(self):
	#	pass

	def prepare(self):
		try:
			self.__checkAuth(self.request.headers['Authorization'])
		except KeyError:
			# No Authorization Header present. No Access.
			return self.error('AccessDenied')
		
	# Version 2: http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html
	def __checkAuth(self, authheader):
		try:
			Version, AWSAccess = authheader.strip().split(" ")
		except ValueError:
			return self.error('AccessDenied')
		if not Version == 'AWS': # yet not supporting AWS4
			return self.error('AccessDenied')
		try:
			AWSAccessKeyId, Signature = AWSAccess.split(':')
		except ValueError:
			return self.error('AccessDenied')

		authenticator = AWSAuth(AWSAccessKeyId, 'secret', 'localhost')
		if authenticator.get_signature(self.request.uri, self.request.headers, self.request.method) != Signature:
			return self.error('SignatureDoesNotMatch')
			
	def getCreationDate(self, fso):
		return str(datetime.datetime.utcfromtimestamp(os.stat(fso).st_ctime))
		
	def getModificationDate(self, fso):
		return str(datetime.datetime.utcfromtimestamp(os.stat(fso).st_mtime))
	
	def getFileSize(self, fso):
		return os.stat(fso).st_size

	def getETag(self, fso):
		if os.path.exists(fso) and os.path.isfile(fso):
			return hashlib.md5(open(fso).read()).hexdigest()
		else:
			return hashlib.md5(fso).hexdigest()
			
	def error(self, code, resource='', requestid='', hostid=''):
		self.set_header("Content-Type", "application/xml; charset=UTF-8")
		ae = AWSError(code)
		error = ({
			"Code": ae.getKey(),
			"Message": ae.getMessage(),
			"Resource": self.get_argument('Resource', default="?"),
			"RequestId": self.get_argument('RequestId', default="?"),
			"HostId": self.get_argument('HostId', default="?"),
		})
		self.set_status(ae.getCode())
		return self.render("templates/ErrorResponse.xml", error=error)
		
	def _getOwner(self, bucket = None, name = None): # Pseudo-Function
		return {"ID": "F673467", "DisplayName": "alexander.bredo@edag.de"}
	
	def _getACL(self, bucket = None, name = None): # Pseudo-Function
		self.set_header("Content-Type", "application/xml; charset=UTF-8")
		owner = self._getOwner(bucket, name)
		grant = {"Permission": "FULL_CONTROL"} 
		return self.render("templates/AccessControlPolicy.xml", owner=owner, grant=grant)
		
	def _getLocation(self, bucket = None, name = None): # Pseudo-Function
		self.set_header("Content-Type", "application/xml; charset=UTF-8")
		return self.render("templates/LocationConstraint.xml", Location='EU')

		
class RootHandler(BaseHandler):
	SUPPORTED_METHODS = ("GET")
	
	def get(self):
		self.set_header("Content-Type", "application/xml; charset=UTF-8")
		buckets = []
		for name in os.listdir(self.application.directory):
			path = os.path.join(self.application.directory, name)
			buckets.append({
				"Name": name,
				"CreationDate": self.getCreationDate(path)
			})
		owner = self._getOwner()
		return self.render("templates/ListAllMyBucketsResult.xml", buckets=buckets, owner=owner)

class BucketHandler(BaseHandler):
	SUPPORTED_METHODS = ("GET", "HEAD", "PUT", "DELETE")
	
	def head(self, bucket):
		self.set_status(200)
		
	def get(self, bucket):
		bucketpath = os.path.abspath(os.path.join(self.application.directory, bucket))
		prefix = self.get_argument('prefix', default="")
		path = os.path.join(bucketpath, prefix)
		
		if not os.path.exists(path):
			return self.error('NoSuchBucket', bucket)
			
		if 'acl' in self.request.arguments:
			return self._getACL(bucket)
		elif 'location' in self.request.arguments:
			return self._getLocation(bucket)
		elif 'logging' in self.request.arguments:
			return self.__getLogging(bucket)
		else:
			self.set_header("Content-Type", "application/xml; charset=UTF-8")
			return self.__getContents(bucket, prefix, path) # _getContentsRecursive (???)

	def __getContents(self, bucket, prefix, path):
		contents = []
		directories = []
		for fso in os.listdir(path):
			fsoPath = os.path.join(path, fso)
			if os.path.isfile(fsoPath):
				contents.append({
					"Key": (prefix + '/' + fso).strip('/'),
					"LastModified": self.getModificationDate(fsoPath),
					"ETag": self.getETag(fsoPath),
					"Size": str(self.getFileSize(fsoPath)),
					"Owner": self._getOwner(bucket),
					"StorageClass": "STANDARD",
				})
			else:
				directories.append((prefix + '/' + fso).strip('/'))
		return self.render("templates/ListBucketResult.xml", contents=contents, directories=directories, Name=bucket, Prefix=prefix)
		
	def __getContentsRecursive(self, bucket, prefix, path):
		contents = []
		directories = []
		for root, dirs, files in os.walk(path):
			relpath = root.replace(bucketpath + '\\', '').replace('\\', '/').strip()
			if relpath and relpath != prefix:
				directories.append(relpath)
			
			for file in files:
				fsoPath = os.path.join(bucketpath, root, file)
				contents.append({
					"Key": (relpath + '/' + file).strip('/'),
					"LastModified": self.getModificationDate(fsoPath),
					"ETag": self.getETag(fsoPath),
					"Size": str(self.getFileSize(fsoPath)),
					"Owner": self._getOwner(bucket),
					"StorageClass": "STANDARD",
				})
		return self.render("templates/ListBucketResult.xml", contents=contents, directories=directories, Name=bucket, Prefix=prefix)
	
	def __getLogging(self, bucket):
		self.set_header("Content-Type", "application/xml; charset=UTF-8")
		return self.render("templates/BucketLoggingStatus.xml")
		
	def put(self, bucket):
		path = os.path.abspath(os.path.join(self.application.directory, bucket))
		if not os.path.exists(path):
			os.makedirs(path)
			self.finish()
		else:
			return error("BucketAlreadyExists", bucket)
		
	def delete(self, bucket):
		path = os.path.abspath(os.path.join(self.application.directory, bucket))
		if not os.path.exists(path):
			return self.error('NoSuchBucket', bucket)
		if not os.path.isfile(path):
			shutil.rmtree(path) # recursive delete (other than in Original AWS!)
		self.set_status(204)
		self.finish()
		
class ObjectHandler(BaseHandler):
	SUPPORTED_METHODS = ("GET", "HEAD", "PUT", "DELETE")
	
	def head(self, bucket, name):
		self.set_status(200)
		
	def get(self, bucket, name):
		path = os.path.abspath(os.path.join(self.application.directory, bucket, name))
		if 'acl' in self.request.arguments:
			return self._getACL(bucket, name)
		elif 'location' in self.request.arguments:
			return self._getLocation(bucket, name)
		else:
			if not os.path.exists(path):
				return self.error('NoSuchKey', bucket + '/' + name)
			if os.path.isfile(path):
				return self.__getFile(path)
			else:
				return self.__getSubdirectory(bucket, name)
				
	def __getFile(self, path):
		self.set_header("Content-Type", "application/octet-stream")
		ofile = open(path, "rb")
		try:
			self.set_status(200)
			self.finish(ofile.read())
		except:
			raise web.HTTPError(404)
		finally:
			ofile.close()
	
	def __getSubdirectory(self, bucket, name):
		return self.redirect('/' + bucket + '?prefix=' + name, permanent=False)
	
	def put(self, bucket, name):
		path = os.path.abspath(os.path.join(self.application.directory, bucket, name))
		if len(self.request.body.strip()) == 0:
			if not os.path.exists(path):
				os.makedirs(path)
		else:
			object_file = open(path, "w")
			object_file.write(self.request.body)
			object_file.close()
		self.finish()
			
	def delete(self, bucket, name):
		path = os.path.abspath(os.path.join(self.application.directory, bucket, name))
		if os.path.isfile(path):
			os.remove(path)
		else:
			shutil.rmtree(path) # recursive delete
		self.set_status(204)
		self.finish()
		
		
if __name__ == "__main__":
	try:
		print("Running. Stop with CTRL+Pause...")
		application = S3Server("./storage")
		http_server = httpserver.HTTPServer(application, ssl_options={
			"certfile": os.path.join('keys', "http.public.key"),
			"keyfile": os.path.join('keys', "http.private.key"),
		})
		http_server.listen(443)
		io_loop = ioloop.IOLoop.instance()
		autoreload.start(io_loop)
		io_loop.start()
	except KeyboardInterrupt:
		ioloop.IOLoop.instance().stop()
		print("End of Service")