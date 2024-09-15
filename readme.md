# Cogito x Infor

<div align="center">
    <img src="docs/images/infor.png" width="50%" alt="Cogito Image" style="display: block; margin-left: auto; margin-right: auto;">
</div>

## Description

This project is a collaboration between Cogito and [Infor AS](https://www.infor.com/nordics), aimed at exploring and developing recommendation systems. Our partnership has so far resulted in a fully-functioning MVP on our own custom test-website. The website contains sample-products fetched from Amazon, and will recommend similar products to the one the user clicks on, so called "cross-sell"-recommendation. Further development will be in collaboration with one of Infors clients, and our goal is to help them make use of AI-powered recommendation systems to recommend relevant products to their customers in order to drive growth.

### Prerequisites

- Ensure that Git is installed on your machine. [Download Git](https://git-scm.com/downloads)
- Ensure that Git LFS is installed on your machine. [Download Git LFS](https://git-lfs.com)
- Docker is used for building the entire application. [Download Docker](https://www.docker.com/products/docker-desktop)

### Configuration

Start by making a copy of the `.env.example` file and renaming it to `.env`. This file contains the environment variables that the application needs to run. You can change the values of the variables to match your environment.

Run the following command in the root folder to copy the `.env.example` file:

```bash
cp .env.example .env
```

Then, replace the placeholder values with your own values in the `.env` file. You can generate an API-key [here](https://developers.google.com/custom-search/v1/introduction)

## Usage

To run the project run the following command in the root folder:

```bash
docker-compose up --build
```

## Contributors

This project would not have been possible without the hard work and dedication of all of the contributors. Thank you for the time and effort you have put into making TutorAI a reality.

<table align="center">
  <tr>
    <td align="center">
        <a href="https://github.com/Spiderpig02">
            <img src="https://github.com/Spiderpig02.png?size=100" width="100px;" alt="Daniel Neukirch Hansen"/><br />
            <sub><b>Daniel Neukirch Hansen</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/thomsoren">
            <img src="https://github.com/thomsoren.png?size=100" width="100px;" alt="Thomas Sørensen"/><br />
            <sub><b>Thomas Sørensen</b></sub>
        </a>
    <td align="center">
        <a href="https://github.com/jmnorheim">
            <img src="https://github.com/jmnorheim.png?size=100" width="100px;" alt="Jens Martin Norheim Berget"/><br />
            <sub><b>Jens Martin Norheim Berget</b></sub>
        </a>
    <td align="center">
        <a href="https://github.com/bjorneme">
            <img src="https://github.com/bjorneme.png?size=100" width="100px;" alt="Bjørn Melaaen"/><br />
            <sub><b>Bjørn Melaaen</b></sub>
        </a>
    <td align="center">
        <a href="https://github.com/NikolaiHelleseth">
            <img src="https://github.com/NikolaiHelleseth.png?size=100" width="100px;" alt="Nikolai Helgås Helleseth"/><br />
            <sub><b>Nikolai Helgås Helleseth</b></sub>
        </a>
    <td align="center">
        <a href="https://github.com/09august">
            <img src="https://github.com/09august.png?size=100" width="100px;" alt="August Myhre"/><br />
            <sub><b>August Myhre</b></sub>
        </a>
    <td align="center">
        <a href="https://github.com/HamidOAI">
            <img src="https://github.com/HamidOAI.png?size=100" width="100px;" alt="Hamid"/><br />
            <sub><b>Hamid</b></sub>
        </a>
    <td align="center">
        <a href="https://github.com/Vebjorn999999999999999">
            <img src="https://github.com/Vebjorn999999999999999.png?size=100" width="100px;" alt="Vebjørn Kittelsen Bergh"/><br />
            <sub><b>Vebjørn Kittelsen Bergh</b></sub>
        </a>
    <td align="center">
        <a href="https://github.com/abdihake">
            <img src="https://github.com/abdihake.png?size=100" width="100px;" alt="Abdihakim Elmi"/><br />
            <sub><b>Abdihakim Elmi</b></sub>
        </a>
    </td>
  </tr>
</table>
