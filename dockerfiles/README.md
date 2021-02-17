```
                    ##        .            
              ## ## ##       ==            
           ## ## ## ##      ===            
       /""""""""""""""""\___/ ===        
  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
       \______ o          __/            
         \    \        __/             
          \____\______/                
 
          |          |
       __ |  __   __ | _  __   _
      /  \| /  \ /   |/  / _\ | 
      \__/| \__/ \__ |\_ \__  |
```
TODO:
- [ ] Check if there is a lighter image available (or it does not matter?)
- [ ] maybe fix the naming of the files

 * base: pulls Ubuntu 18.04 and install a bunch of packages
 * server: base + an entry point directly starting iot\process_data.py
 * classifier: base + an entry point directly starting iot\iot_classifier.py