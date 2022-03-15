links=[
      {
        "source": "15", 
        "target": "1", 
        "value": 2
      }, 
      {
        "source": "0", 
        "target": "1", 
        "value": 2
      }, 
      {
        "source": "6", 
        "target": "1", 
        "value": 2
      }, 
      {
        "source": "16", 
        "target": "4", 
        "value": 2
      }, 
      {
        "source": "1", 
        "target": "4", 
        "value": 2
      }, 
      {
        "source": "11", 
        "target": "4", 
        "value": 2
      }, 
      {
        "source": "5", 
        "target": "4", 
        "value": 2
      }, 
      {
        "source": "19", 
        "target": "6", 
        "value": 2
      }, 
      {
        "source": "18", 
        "target": "15", 
        "value": 2
      }, 
      {
        "source": "17", 
        "target": "16", 
        "value": 2
      }
    ]

res=list()

for ele in links:
  res.append(int(ele['source']))
  res.append(int(ele['target']))

res=list(set(res))
print (res)