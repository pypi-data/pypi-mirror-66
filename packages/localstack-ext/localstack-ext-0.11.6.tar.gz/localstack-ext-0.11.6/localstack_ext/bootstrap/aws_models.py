from localstack.utils.aws import aws_models
GSHmY=super
GSHmV=None
GSHmy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GSHmY(LambdaLayer,self).__init__(arn)
  self.cwd=GSHmV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,GSHmy,env=GSHmV):
  GSHmY(RDSDatabase,self).__init__(GSHmy,env=env)
 def name(self):
  return self.GSHmy.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
