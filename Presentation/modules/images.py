def display(image):
   
    from PIL import Image
    import requests
    im ='Enter a valid image name'
    
    
    
    if image == 'plane':
        url = 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1053&q=80'
        return Image.open(requests.get(url, stream=True).raw)
    
    
    
    
    if image == 'workflow':
        
        from IPython.display import Image
        return Image('images/Workflow.png')
             
        
    if image == 'basic':
        
        from IPython.display import Image
        return Image('images/BasicModel.png')
    
    
    if image == 'complex':
        
        from IPython.display import Image
        return Image('images/ComplexModel.png')
    
    
    
    if image == 'challenges':
        
        from IPython.display import Image
        return Image('images/Challenges.png')