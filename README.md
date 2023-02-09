# sparking

## Getting Started

This project contains a docker-compose.yml file, which is intended to be used
during development to launch all necessary dependencies.

```shell script
docker-compose up 
```

### Answer

1. Please take a look at Simple-architectore.drawio.png
3. I prefer REST combined with message queuing, such as rabbitmq or others. 
   Reason: 
    - REST API is easier to maintain but it also depends on the difficulties 
      (I have read case such as slack chat that may ban someone from certain group 
       but doesn't make that user banned forever - just a certain group chat)
    - REST API also easier to elaborate to the other related team member such 
      as mobile team and frontend team.
    - cons for using REST and message queue if rabbitmq service happens to face 
      problems there will be data gap since related parties can't send and 
      subscribe - consume.
4. Structural composite, reason is because easier to be worked on.