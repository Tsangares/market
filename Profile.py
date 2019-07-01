import yaml
myBusiness="profile.yaml"
with open(myBusiness, 'r') as f:
    myBusiness=yaml.safe_load(f.read())
    
