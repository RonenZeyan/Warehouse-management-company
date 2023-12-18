

let DeleteButton = document.getElementById('deleteBut')

function Confirm(){
    if(confirm('Are you Sure you want to delete?')){
        DeleteButton.setAttribute("'href'","{{url_for('delete_post',title=post.title)}}")
        href=""
    }
    else{

    }
}