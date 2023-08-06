from localstack.utils.aws import aws_models
nBHTJ=super
nBHTu=None
nBHTL=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nBHTJ(LambdaLayer,self).__init__(arn)
  self.cwd=nBHTu
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,nBHTL,env=nBHTu):
  nBHTJ(RDSDatabase,self).__init__(nBHTL,env=env)
 def name(self):
  return self.nBHTL.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
