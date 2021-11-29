
  let searchForm= document.getElementById('searchForm');
  let pageLinks = document.getElementsByClassName('btn-link');

  // ensure searchform exist
 
  if(searchForm){
    for (let i=0; pageLinks.length > i; i++) {
      pageLinks[i].addEventListener('click', function(e){
        e.preventDefault();
        // get the page attribute
        let page = this.dataset.page
        // add hidden input field
        searchForm.innerHTML += `<input value=${page} name='page' hidden />`
  
         // submit the form 
         searchForm.submit()
      })
    }
   }

   
   let tags = document.getElementsByClassName('project-tag')
   for (const tag of tags){
     tag.addEventListener('click', function(e){
       let tagId = e.target.dataset.tag
       let projectId = e.target.dataset.project
       
       fetch('http://127.0.0.1:8000/api/remove-tag/', {
 
         method: 'DELETE',
         headers: {
           'Content-Type': 'application/json'
         },
         body: JSON.stringify({'project':projectId, 'tag':tagId})
       }).then(response => response.json())
       .then(data => {
         e.target.remove()
       })
 
     })
   }