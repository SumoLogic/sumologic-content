# delete_ghost_collectors
Delete offline collectors

## Requirements
Python 3
Sumo Logic API Access ID and key created

### Arguments
- Deployment - API deployment
- Access ID - API Access ID
- Password - API Access Key
- Hours Offline - number of hours collectors have been inactive
- Audit Mode - (y/n)  
  - y - print name of collectors on terminal without deleting the collectors
  - n - print and delete collectors on terminal

#### Execution
`# python delete_ghost_collectors.py`

You'll be prompted to enter the Arguments. 
