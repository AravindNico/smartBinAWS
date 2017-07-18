# Smart bin - UI - Simulation 

      1 . Smartbin trash filling simulation
      2 . Smartbin AutoRouting

## prerequisite:

1.Change the google map api key in the [index.html](https://github.com/AravindNico/smartBinAWS/blob/master/UI/index.html) page line number 45<br>
2.Provide your AWS id's and smart bin settings in [awsConfig.json](https://github.com/AravindNico/smartBinAWS/blob/master/UI/awsConfig.json) file.<br>

## Program Execution:

1.Open the <strong>index.html</strong> file in any browser , you can see the mqtt connection getting connected with temporary credentials provided by conito service.<br>
2.Execute [BinOperation](https://github.com/AravindNico/smartBinAWS/tree/master/binOperation) script which simulates the bin filling scenario.<br>
3.Once the bins reaches binPickUp threshold , click on the submit Query button , this generates optimized route between the bins which are above pickup threshold.<br>

## Pickup executions
Pick up operation can be done through two ways , any one step can be used 

### Through UI

Click on the pickup button , which clears all the bins in routing order.

### Through Python Script

Open the [binpickupOperation](https://github.com/AravindNico/smartBinAWS/tree/master/pickupOperation) script and execute the pickupOperation script.

  
      
 
