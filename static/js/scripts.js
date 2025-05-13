function write_answer(answer)
{
    let antwort = document.querySelector("#antwort");
    antwort.innerText = answer ;
}

function greet(event)
{
    let name = document.querySelector("#name").value;
    write_answer("Hello, " + name);
    event.preventDefault();
}

function keyecho(field)
{
    let name = document.querySelector(field);
    name.addEventListener('keyup', function(event)
    {
        if (name.value)
        {
            write_answer(`Hello, ${name.value}`);
        }
        else
        {
            write_answer("Hello, whoever you are");
        }
    })
}

document.addEventListener('DOMContentLoaded',
    function()
    {
        try {

            let form = document.querySelector("form");
            form.addEventListener("submit", greet);
            keyecho("#name");
        }
        catch (err) {}
        let fileName = location.href.split("/").slice(-1);
        let now = new Date();
        let currentTime = now.toLocaleTimeString('en-US',
            { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        let day = String(now.getDate()).padStart(2, "0");
        let month = String(now.getMonth() + 1).padStart(2, "0");
        let year = now.getFullYear();
        let datestr  = year + "-" + month + "-" + day;
        let dtstring = datestr + " " + currentTime;
        fileName = fileName + " " + dtstring ;
        try {
            document.querySelector("#filename").innerText = fileName;
        }
        catch (err) {}
    }
)


