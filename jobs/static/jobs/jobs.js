document.addEventListener('DOMContentLoaded', () => {

      var x = window.matchMedia("(min-width: 650px)")

      // Set links up to load job section.
      document.querySelectorAll('.job-link').forEach(link => {
          link.onclick = () => {
              const job_id = link.dataset.page;
              document.querySelector('#job-title').innerHTML = "";
              document.querySelector('#job-content').innerHTML = "";
              document.querySelector('#job-apply').innerHTML = "";
              loadjob(job_id)
              return false;
          };
      });

      // Set links up to save job for user.
      // document.querySelectorAll('.userjob-link').forEach(link => {
      //     link.onclick = () => {
      //         const job_id = link.dataset.page;
      //         postjob(job_id)
      //         alert("Job has been saved to your profile.");
      //         return false;
      //     };
      // });

      // Load specific job.
      function loadjob(id) {
          url = 'https://www.themuse.com/api/public/jobs/'+id

          const request = new XMLHttpRequest();
          request.open('GET', url);
          request.onload = () => {
              const data = JSON.parse(request.responseText);
              title = data["name"]
              company = data["company"]["name"]
              content = data["contents"]
              apply = data["refs"]["landing_page"]

              jobtitle = "<span class=\"p-comp\">Company: <b>"+company+"</b></span><br><span class=\"p-left\"><h3>"+title+"</h3></span><br><span class=\"p-right\"></span><hr>"
              jobcontent = "<span>"+content+"</span><br>"
              button = "<a href=\""+apply+"\"  target=\"_blank\" class=\"btn btn-mybtn btn-lg\" role=\"button\" aria-pressed=\"true\">Apply</a>"

              document.querySelector('#job-title').innerHTML += jobtitle;
              document.querySelector('#job-content').innerHTML += jobcontent;
              document.querySelector('#job-apply').innerHTML += button;
          };
          request.send()
      };

      // function postjob(id) {
      //     const request = new XMLHttpRequest();
      //     request.open('Post', '/user_map');
      //     request.onload = () => {
      //         const data = JSON.parse(request.responseText);
      //     };
      //     const data = new FormData();
      //     data.append('job_id', id);
      //     for (var p of data) {
      //       console.log(p);
      //     }
      //     request.send(data)
      // };
      //
      // function deletejob(id) {
      //     const request = new XMLHttpRequest();
      //     request.open('Post', '/delete');
      //     request.onload = () => {
      //         const data = JSON.parse(request.responseText);
      //     };
      //     const data = new FormData();
      //     data.append('job_id', id);
      //     for (var p of data) {
      //       console.log(p);
      //     }
      //     request.send(data)
      // };
      //
      // function validateRegister() {
      //     var x = document.forms["register"]["username"].value;
      //     var y = document.forms["register"]["password"].value;
      //     var z = document.forms["register"]["email"].value;
      //     if (x == "" || y == "" || z == "") {
      //       alert("username, password and email must be filled out");
      //       return false;
      //     }
      //   };
});
