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

# -*- coding: utf-8 -*-

defAWSerrors = dict()
defAWSerrors["AccessDenied"] = ("Access Denied",403)
defAWSerrors["AccountProblem"] = ("There is a problem with your AWS account that prevents the operation from completing successfully. Please use Contact Us.",403)
defAWSerrors["AmbiguousGrantByEmailAddress"] = ("The e-mail address you provided is associated with more than one account.",400)
defAWSerrors["BadDigest"] = ("The Content-MD5 you specified did not match what we received.",400)
defAWSerrors["BucketAlreadyExists"] = ("The requested bucket name is not available. The bucket namespace is shared by all users of the system. Please select a different name and try again.",409)
defAWSerrors["BucketAlreadyOwnedByYou"] = ("Your previous request to create the named bucket succeeded and you already own it.",409)
defAWSerrors["BucketNotEmpty"] = ("The bucket you tried to delete is not empty.",409)
defAWSerrors["CredentialsNotSupported"] = ("This request does not support credentials.",400)
defAWSerrors["CrossLocationLoggingProhibited"] = ("Cross location logging not allowed. Buckets in one geographic location cannot log information to a bucket in another location.",403)
defAWSerrors["EntityTooSmall"] = ("Your proposed upload is smaller than the minimum allowed object size.",400)
defAWSerrors["EntityTooLarge"] = ("Your proposed upload exceeds the maximum allowed object size.",400)
defAWSerrors["ExpiredToken"] = ("The provided token has expired.",400)
defAWSerrors["IllegalVersioningConfigurationException"] = ("Indicates that the Versioning configuration specified in the request is invalid.",400)
defAWSerrors["IncompleteBody"] = ("You did not provide the number of bytes specified by the Content-Length HTTP header",400)
defAWSerrors["IncorrectNumberOfFilesInPostRequest"] = ("POST requires exactly one file upload per request.",400)
defAWSerrors["InlineDataTooLarge"] = ("Inline data exceeds the maximum allowed size.",400)
defAWSerrors["InternalError"] = ("We encountered an internal error. Please try again.","500 Internal Server Error")
defAWSerrors["InvalidAccessKeyId"] = ("The AWS Access Key Id you provided does not exist in our records.",403)
defAWSerrors["InvalidAddressingHeader"] = ("You must specify the Anonymous role.",400)
defAWSerrors["InvalidArgument"] = ("Invalid Argument",400)
defAWSerrors["InvalidBucketName"] = ("The specified bucket is not valid.",400)
defAWSerrors["InvalidBucketState"] = ("The request is not valid with the current state of the bucket.",409)
defAWSerrors["InvalidDigest"] = ("The Content-MD5 you specified was an invalid.",400)
defAWSerrors["InvalidLocationConstraint"] = ("The specified location constraint is not valid. For more information about Regions, see How to Select a Region for Your Buckets.",400)
defAWSerrors["InvalidObjectState"] = ("The operation is not valid for the current state of the object.",403)
defAWSerrors["InvalidPart"] = ("One or more of the specified parts could not be found. The part might not have been uploaded, or the specified entity tag might not have matched the part's entity tag.",400)
defAWSerrors["InvalidPartOrder"] = ("The list of parts was not in ascending order.Parts list must specified in order by part number.",400)
defAWSerrors["InvalidPayer"] = ("All access to this object has been disabled.",403)
defAWSerrors["InvalidPolicyDocument"] = ("The content of the form does not meet the conditions specified in the policy document.",400)
defAWSerrors["InvalidRange"] = ("The requested range cannot be satisfied.",416)
defAWSerrors["InvalidRequest"] = ("SOAP requests must be made over an HTTPS connection.",400)
defAWSerrors["InvalidSecurity"] = ("The provided security credentials are not valid.",403)
defAWSerrors["InvalidSOAPRequest"] = ("The SOAP request body is invalid.",400)
defAWSerrors["InvalidStorageClass"] = ("The storage class you specified is not valid.",400)
defAWSerrors["InvalidTargetBucketForLogging"] = ("The target bucket for logging does not exist, is not owned by you, or does not have the appropriate grants for the log-delivery group.",400)
defAWSerrors["InvalidToken"] = ("The provided token is malformed or otherwise invalid.",400)
defAWSerrors["InvalidURI"] = ("Couldn't parse the specified URI.",400)
defAWSerrors["KeyTooLong"] = ("Your key is too long.",400)
defAWSerrors["MalformedACLError"] = ("The XML you provided was not well-formed or did not validate against our published schema.",400)
defAWSerrors["MalformedPOSTRequest"] = ("The body of your POST request is not well-formed multipart/form-data.",400)
defAWSerrors["MalformedXML"] = ("This happens when the user sends a malformed xml (xml that doesn't conform to the published xsd) for the configuration. The error message is: The XML you provided was not well-formed or did not validate against our published schema.",400)
defAWSerrors["MaxMessageLengthExceeded"] = ("Your request was too big.",400)
defAWSerrors["MaxPostPreDataLengthExceededError"] = ("Your POST request fields preceding the upload file were too large.",400)
defAWSerrors["MetadataTooLarge"] = ("Your metadata headers exceed the maximum allowed metadata size.",400)
defAWSerrors["MethodNotAllowed"] = ("The specified method is not allowed against this resource.",405)
defAWSerrors["MissingAttachment"] = ("A SOAP attachment was expected, but none were found.",400)
defAWSerrors["MissingContentLength"] = ("You must provide the Content-Length HTTP header.",411)
defAWSerrors["MissingRequestBodyError"] = ("This happens when the user sends an empty xml document as a request. The error message is: Request body is empty.",400)
defAWSerrors["MissingSecurityElement"] = ("The SOAP 1.1 request is missing a security element.",400)
defAWSerrors["MissingSecurityHeader"] = ("Your request was missing a required header.",400)
defAWSerrors["NoLoggingStatusForKey"] = ("There is no such thing as a logging status sub-resource for a key.",400)
defAWSerrors["NoSuchBucket"] = ("The specified bucket does not exist.",404)
defAWSerrors["NoSuchKey"] = ("The specified key does not exist.",404)
defAWSerrors["NoSuchLifecycleConfiguration"] = ("The lifecycle configuration does not exist.",404)
defAWSerrors["NoSuchUpload"] = ("The specified multipart upload does not exist. The upload ID might be invalid, or the multipart upload might have been aborted or completed.",404)
defAWSerrors["NoSuchVersion"] = ("Indicates that the version ID specified in the request does not match an existing version.",404)
defAWSerrors["NotImplemented"] = ("A header you provided implies functionality that is not implemented.",501)
defAWSerrors["NotSignedUp"] = ("Your account is not signed up for the S3 service. You must sign up before you can use S3.",403)
defAWSerrors["NotSuchBucketPolicy"] = ("The specified bucket does not have a bucket policy.",404)
defAWSerrors["OperationAborted"] = ("A conflicting conditional operation is currently in progress against this resource. Please try again.",409)
defAWSerrors["PermanentRedirect"] = ("The bucket you are attempting to access must be addressed using the specified endpoint. Please send all future requests to this endpoint.",301)
defAWSerrors["PreconditionFailed"] = ("At least one of the preconditions you specified did not hold.",412)
defAWSerrors["Redirect"] = ("Temporary redirect.",307)
defAWSerrors["RestoreAlreadyInProgress"] = ("Object restore is already in progress.",409)
defAWSerrors["RequestIsNotMultiPartContent"] = ("Bucket POST must be of the enclosure-type multipart/form-data.",400)
defAWSerrors["RequestTimeout"] = ("Your socket connection to the server was not read from or written to within the timeout period.",400)
defAWSerrors["RequestTimeTooSkewed"] = ("The difference between the request time and the server's time is too large.",403)
defAWSerrors["RequestTorrentOfBucketError"] = ("Requesting the torrent file of a bucket is not permitted.",400)
defAWSerrors["SignatureDoesNotMatch"] = ("The request signature we calculated does not match the signature you provided. Check your AWS Secret Access Key and signing method. For more information, see REST Authentication and SOAP Authentication for details.",403)
defAWSerrors["ServiceUnavailable"] = ("Please reduce your request rate.",503)
defAWSerrors["SlowDown"] = ("Please reduce your request rate.",503)
defAWSerrors["TemporaryRedirect"] = ("You are being redirected to the bucket while DNS updates.",307)
defAWSerrors["TokenRefreshRequired"] = ("The provided token must be refreshed.",400)
defAWSerrors["TooManyBuckets"] = ("You have attempted to create more buckets than allowed.",400)
defAWSerrors["UnexpectedContent"] = ("This request does not support content.",400)
defAWSerrors["UnresolvableGrantByEmailAddress"] = ("The e-mail address you provided does not match any account on record.",400)
defAWSerrors["UserKeyMustBeSpecified"] = ("The bucket POST must contain the specified field name. If it is specified, please check the order of the fields.",400)


class AWSError():
	def __init__(self, key):
		if key in defAWSerrors.keys():
			self.key = key
		else:
			self.key = 'AccountProblem'
			
	def getKey(self):
		return self.key 
		
	def getMessage(self):
		return defAWSerrors[self.key][0]
		
	def getCode(self):
		return defAWSerrors[self.key][1]