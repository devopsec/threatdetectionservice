# Threat Management Platfrom GUI

## Goal

To build an easy to use web interface for managing the platform, with a focus on

- Multi-Company: should support multiple companies with multiple soc administrators at different locations
- Agent Management: ability to manage the configuration of agents that are located at different locations
- Threat Notifications: based on information enriched by the enrichment threat intel toplogoies
- User Management: ability to manage users and how they should be notified when a threat occurs 

## Design Principles

- The GUI should not contain any business logic.  
- API calls should be used to drive the GUI.  
- The GUI and API could reside on different machines.  So, the API server URL should be a parameter

## Framework

We are going to use [web2py](http://www.web2py.com/) as the framework because it provides all of the scaffolding needed to build
a web application quickly
