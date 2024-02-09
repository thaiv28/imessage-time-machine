<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->





<div align="center">
<h3 align="center">Text Time Machine</h3>

  <p align="center">
    A website that will display archived iMessage conversations that users can upload.

  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]]()
 A demo of the website is available on https://textmachine.onrender.com.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python
* Flask
* SQLite
* SQLAlchemy
* Waitress
* HTML, CSS

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps. All commands
should be run from inside of the `imessage-time-machine/imessage_time_machine` folder unless otherwise
stated.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/thaiv28/imessage-time-machine.git
   ```
2. Install pip packages
   ```sh
   pip3 install -r ../requirements.txt
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Download archived messages
Use the following docs to create backups for your messages using different 
software.

- [iMazing (Paid)](./docs/backups/imazing.md)

The backup must be stored in the root folder, titled `backup.txt`.


### Initializing Database
1. In `__init__.py`, ensure that the following lines of code
are present.

    ```python
        db.drop_all()
        db.create_all()
        db_service.init_messages(file="backup.txt")
    ```
2. Start server

    ```sh
    flask run
    ```
This should initialize the SQLite database with the proper messages. After the 
database is initialized, you should delete those lines of code from `__init__.py`,
to avoid initializing the database everytime the website is started up.


### Initializing Logins
For more information on setting up a username and password for 
the website, see [Initializing Logins](./docs/login.html).



### Usage
To run the website locally, run the following command

    flask run

### Deployment

To deploy the website, use the command inside of the `imessage_time_machine` folder:
  
    waitress-serve app:app


For more information, visit [Flask's documentation](https://flask.palletsprojects.com/en/2.3.x/deploying/waitress/) to deploy the website using Waitress.


<!-- ROADMAP -->
## Roadmap

- Initializing database through command line argument
- Adding feature to search by date
- Add support for other backup applications

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/thaiv28/imessage-time-machine.svg?style=for-the-badge
[contributors-url]: https://github.com/thaiv28/imessage-time-machine/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/thaiv28/imessage-time-machine.svg?style=for-the-badge
[forks-url]: https://github.com/thaiv28/imessage-time-machine/network/members
[stars-shield]: https://img.shields.io/github/stars/thaiv28/imessage-time-machine.svg?style=for-the-badge
[stars-url]: https://github.com/thaiv28/imessage-time-machine/stargazers
[issues-shield]: https://img.shields.io/github/issues/thaiv28/imessage-time-machine.svg?style=for-the-badge
[issues-url]: https://github.com/thaiv28/imessage-time-machine/issues
[license-shield]: https://img.shields.io/github/license/thaiv28/imessage-time-machine.svg?style=for-the-badge
[license-url]: https://github.com/thaiv28/imessage-time-machine/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: docs/images/example.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 