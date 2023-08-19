# ML Project

#------------------------------------------
- .ebextensions is config for deploying on AWS Elastic BeanStalk. It is a PaaS.
- Inside .ebextensions is a Python config since want to deploy in Python container. The format of that config file is fixed. It requires a start point in our application, named application. That is why we needed to create application.py
- So, for AWS Beanstalk deployment, .ebextensions and application.py are needed.
#------------------------------------------
Similar configuration of application.py is needed for Azure. Azure follows CD
#------------------------------------------