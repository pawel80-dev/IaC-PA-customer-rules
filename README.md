# IaC-PA-customer-rules

> [!NOTE]
> For most of my projects, the leading branch is the **dev** one. That means that *_dev.yaml file is the most frequently used workflow/pipeline.  

The purpose of this project is to demonstrate how to deploy a firewall environment that allows customers to update their own rules via an Excel template, which are then automatically deployed during a controlled change window.  

![alt text](drawings/fw_rules_v01.png)  
*PA customer rules deployment - general design*  

> [!NOTE]
> Mechanism of checking which policy/address group/services should be updated or removed is missing.  