from localstack.utils.aws import aws_models
WMFzl=super
WMFzf=None
WMFzR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  WMFzl(LambdaLayer,self).__init__(arn)
  self.cwd=WMFzf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,WMFzR,env=WMFzf):
  WMFzl(RDSDatabase,self).__init__(WMFzR,env=env)
 def name(self):
  return self.WMFzR.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
