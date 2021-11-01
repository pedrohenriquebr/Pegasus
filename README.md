[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/pedrohenriquebr/Pegasus">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Pegasus</h3>

  <p align="center">
    Finance report
    <br />
    <a href="https://github.com/pedrohenriquebr/Pegasus"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/pedrohenriquebr/Pegasus">View Demo</a>
    ·
    <a href="https://github.com/pedrohenriquebr/Pegasus/issues">Report Bug</a>
    ·
    <a href="https://github.com/pedrohenriquebr/Pegasus/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

### Built With

* [Python 3.9.5](https://www.python.org/downloads/release/python-395/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/index.html)
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/pedrohenriquebr/Pegasus.git
   ```
2. Install packages
   ```sh
   pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
## Usage


Fill the `template.xlsx` with needed information
The tab `categorias` with each category following child category
The tab `historico` is where you  associative table, the column HISTORICO contains the name
and CATEGORIA for the sub category.

After that, call the main script via CLI.

```bash
foo@bar$ python main.py --filename extrato_template.xlsx
```

> the first time you use the script, add --filename in prompt for load initial data.
> for future data loading, check the extrato_template.csv if it was following the template schema

the finance report will be in the same template.xlsx file on `report` tab


_For more examples, please refer to the [Documentation](https://example.com)_


# Usage

## local environment

```bash
$ pip install -r requirements.dev.txt
$ waitress-serve --listen=*:8000 wsgi:app 
```

## Unix-like environment

```bash
$ pip install -r requirements.txt
$ gunicorn wsgi:app
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/github_username/repo_name/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL-2 License. See `LICENSE` for more information.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()



[contributors-shield]: https://img.shields.io/github/contributors/pedrohenriquebr/Pegasus.svg?style=for-the-badge
[contributors-url]: https://github.com/pedrohenriquebr/Pegasus/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/pedrohenriquebr/Pegasus.svg?style=for-the-badge
[forks-url]: https://github.com/pedrohenriquebr/Pegasus/network/members
[stars-shield]: https://img.shields.io/github/stars/pedrohenriquebr/Pegasus.svg?style=for-the-badge
[stars-url]: https://github.com/pedrohenriquebr/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/pedrohenriquebr/Pegasus.svg?style=for-the-badge
[issues-url]: https://github.com/pedrohenriquebr/Pegasus/issues
[license-shield]: https://img.shields.io/github/license/pedrohenriquebr/Pegasus.svg?style=for-the-badge
[license-url]: https://github.com/pedrohenriquebr/Pegasus/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/pedro-henrique-braga-da-silva
