# Sumo Logic for Software Development Optimization

If your DevOps pipeline has tools that are not supported by Out of the Box toolset of [Software Development Optimization Solution] (https://help.sumologic.com/Other_Solutions/Software_Development_Optimization_Solution/01_About_the_Software_Development_Optimization_Solution) then you can integrate your tool, and map it to the relevant schema model. 

For example, if you were to integrate Azure DevOps, which  provides developer services to support teams to plan work, collaborate on code development, and build and deploy applications, with the SDO solution, you would first:

Install the SDO solution as documented here.

Add SDO field extraction rules, to map events from your tool to the SDO event schema.

We have provided field extraction rules for following offically not supported tools :

1. AzureDevOps
2. CircleCI
3. Gitlab
4. Octopus

Note: These FERs are good starting point, and may need some customization to work. Find/Replace <REPLACE_FOO> with your _sourceCategory before importing them in to Sumo Logic. For more info on FER, please read [here!] (https://help.sumologic.com/Manage/Field-Extractions) 