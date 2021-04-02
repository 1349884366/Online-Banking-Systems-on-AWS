// define aws fetch url
var url = "https://i40c1sj0qc.execute-api.us-east-1.amazonaws.com/dev";
// define login api
var callLogin = (Email,Password)=>{
    // instantiate a headers object
    localStorage.email = Email;
    var myHeaders = new Headers();
    // add content type header to object
    myHeaders.append("Content-Type", "application/json");
    // using built in JSON utility package turn object to string and store in a variable
    var raw = JSON.stringify({"Opeartion": "Login","Email":Email,"Password":Password});
    // create a JSON object with parameters for API call and store in a variable
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    // make API call with parameters and use promises to get response
    fetch(url, requestOptions)
    .then(response => response.text())
    .then(result => login(result))
    .catch(error => console.log('error', error));
}
// define login function
var login = (event) =>{
    msg = JSON.parse(event).body;
    if(msg == null){
        alert('error');
    }
    else{
        body = JSON.parse(msg);
        localStorage.lname = body.name;
        balance = body.balance;
        localStorage.balance = balance;
        localStorage.auth = body.auth;
        logged_in();
        var x = document.getElementById("myDIV");
        x.innerHTML = '<img src="avatar.svg" id = "avatar">'+"<p>Name:"+localStorage.lname+'</p><p id= "balance">Balance:'+balance+'</p>'+
        '<button type="button" class="profile_btn" onclick="openFormTransaction()">Make a transaction</button>'+
        '<button type="button" class="profile_btn" onclick="openFormDepoist()">Make Depoist</button>'+
        '<button type="button" class="profile_btn" onclick="callHis()">View History</button>'+
        '<button type="button" class="profile_btn" onclick="callAct()">View Activities</button>';
        var btn = document.getElementById("open-button");
        btn.innerHTML = "Log-out";
        btn.setAttribute( "onClick", "javascript: logout();" );
    }
}



// define signup api
var callSignup = (Name,Email,Password,CPassword,)=>{
    if(Password != CPassword){
        alert('Password does not match');
        return;
    }
    // instantiate a headers object
    var myHeaders = new Headers();
    // add content type header to object
    myHeaders.append("Content-Type", "application/json");
    // using built in JSON utility package turn object to string and store in a variable
    var raw = JSON.stringify({"Opeartion": "Signup","Name":Name,"Email":Email,"Password":Password});
    // create a JSON object with parameters for API call and store in a variable
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    // make API call with parameters and use promises to get response
    fetch(url, requestOptions)
    .then(response => response.text())
    .then(result => Signup(result))
    .catch(error => console.log('error', error));
}
// define signup function
var Signup = (event) =>{
    msg = JSON.parse(event).body;
    if(JSON.parse(event).statusCode == 401){
        alert(JSON.parse(msg).Description);
    }
    else{
        alert(JSON.parse(msg).Description);
        closeFormSignup();

    }
}

// define the function for logout
var logout = ()=>{
    var btn = document.getElementById("open-button");
    document.getElementById("myDIV").innerHTML = 'Hello'
    btn.innerHTML = "Login";
    btn.setAttribute( "onClick", "javascript: openForm();" );
    document.getElementById("signup").style.display = "block";
    document.getElementById("hello").style.display = "block";
    document.getElementById("myDIV").style.display = "none"
    localStorage.clear();
}

// define Trans api
var callTrans = (reciever,money)=>{
    var auth_key = localStorage.auth;
    var sender = localStorage.email;
    localStorage.new_balance = parseInt(localStorage.balance) - parseInt(money);
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    var raw = JSON.stringify({"Opeartion": "Trans","Sender":sender, "Reciever":reciever, "Money":money, "Auth_key":auth_key});
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    fetch(url, requestOptions)
    .then(response => response.text())
    .then(result => trans(result))
    .catch(error => console.log('error', error));
}
// define Trans function
var trans = (event) =>{
    status_code = JSON.parse(event).statusCode
    msg = JSON.parse(event).body;
    body = JSON.parse(msg);
    if(status_code == 200){
        document.getElementById("balance").innerText ="Balance: "+ localStorage.new_balance;
        localStorage.balance = localStorage.new_balance;
        localStorage.new_balance = null;
        alert(body.Description);
    }
    else{
        alert(body.Description);
    }  
}
// define Deposit api
var callDeposit = (money,attachment )=>{
    var auth_key = localStorage.auth;
    var UserID = localStorage.email;
    var money = money;
    var myHeaders = new Headers();
    localStorage.new_balance = parseInt(localStorage.balance) + parseInt(money);
    myHeaders.append("Content-Type", "application/json");
    var raw = JSON.stringify({"Opeartion": "Deposit","UserID":UserID, "Money":money, "Auth_key":auth_key, "Attachment":attachment});
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    fetch(url, requestOptions)
    .then(response => response.text())
    .then(result => deposit(result))
    .catch(error => console.log('error', error));
}
// define Deposit function
var deposit = (event) =>{
    status_code = JSON.parse(event).statusCode
    msg = JSON.parse(event).body;
    body = JSON.parse(msg);
    if(status_code == 200){
        document.getElementById("balance").innerText ="Balance: "+ localStorage.new_balance;
        localStorage.balance = localStorage.new_balance;
        localStorage.new_balance = null;
        alert(body.Description);
    }
    else{
        alert(body.Description);
    }  
}

var callHis = ()=>{
    var auth_key = localStorage.auth;
    var sender = localStorage.email;
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    var raw = JSON.stringify({"Opeartion": "TransHis","Email":sender,"Auth_key":auth_key});
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    fetch(url, requestOptions)
    .then(response => response.text())
    .then(result => His(result))
    .catch(error => console.log('error', error));
}
var His = (event) =>{
    msg = JSON.parse(event).body;
    body = JSON.parse(msg);
    trans_lst = JSON.parse(body.Transcations);
    localStorage.lst_len = trans_lst.length;
    localStorage.lst = trans_lst;
    localStorage.page = 0;
    openFormHistory();
}

var callAct = ()=>{
    var auth_key = localStorage.auth;
    var sender = localStorage.email;
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    var raw = JSON.stringify({"Opeartion": "Activities","Email":sender,"Auth_key":auth_key});
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    fetch(url, requestOptions)
    .then(response => response.text())
    .then(result => Act(result))
    .catch(error => console.log('error', error));
}
var Act = (event) =>{
    msg = JSON.parse(event).body;
    body = JSON.parse(msg);
    act_lst = JSON.parse(body.Activities);
    localStorage.lst_len = act_lst.length;
    localStorage.lst = act_lst;
    localStorage.page = 0;
    openFormHistory();
}


//define the function for transaction history
function openFormHistory(){
    lst = localStorage.lst.split(",");
    x = document.getElementsByClassName("lst");
    for( i = 0; i<7 ;i++){
        x[i].innerHTML = lst[i+parseInt(localStorage.page)] ;
    }
    document.getElementById("hist_bg").style.display = "block";
}
function next(){
    if ( (parseInt(localStorage.page) + 7) >= (parseInt(localStorage.lst_len)) ){
        alert("This is the last page")
    }
    else{
        localStorage.page = parseInt(localStorage.page)  + 7;
        openFormHistory()
    }
}

function prev(){
    if ( (parseInt(localStorage.page) - 7) < 0 ){
        alert("This is the first page")
    }
    else{
        localStorage.page = parseInt(localStorage.page)  - 7;
        openFormHistory()
    }
}

//define the function for open or close the pop up forms
function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function openFormDepoist(){
    document.getElementById("dep_bg").style.display = "block";
}

function openFormTransaction(){
    document.getElementById("tran_bg").style.display = "block";
}

function closeFormTransaction(){
    document.getElementById("tran_bg").style.display = "none";
}

function openFormSignup(){
    document.getElementById("signForm").style.display = "block";
}

function closeFormSignup(){
    document.getElementById("signForm").style.display = "none";
}

function logged_in(){
    document.getElementById("myDIV").style.display = "block";
    document.getElementById("hello").style.display = "none";
    document.getElementById("myForm").style.display = "none";
    document.getElementById("signForm").style.display = "none";
    document.getElementById("signup").style.display = "none";
}



function closef(){
    document.getElementById("hist_bg").style.display = "none";
    document.getElementById("tran_bg").style.display = "none";
    document.getElementById("dep_bg").style.display = "none";
    localStorage.lst = null;
}



