<h3 align="center">O1 Migration Scripts</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> This repository consist of scripts for data extraction/modification for O1 
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

These Scripts aims to help with the data migration process making it more efficient in the modification and extraction process

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

```
1. Selenium
```

### Installing

A step by step series of examples that tell you how to get a development env running.

Using Python pip install to install selenium
```
pip install selenium
```

## 🎈 Usage <a name="usage"></a>
Run the scripts using the command:
```
python [Script_Name]
```

Note:
Scripts that uses Bentley's API must have new token once in a while,
to generate a new token: 
1. goto [Bentley_Dev](https://developer.bentley.com/apis/forms/operations/get-form-data-details/)
2. Click on "Try it out"
3. Click on the dropdown box "No auth"
4. Select "authorizationCode"
5. Copy the whole line from Authorization under Headers, it starts with "Bearer"
6. Replace the old "Bearer" in the script with the new one in "Authorization" under "HEADERS"

## ✍️ Authors <a name = "authors"></a>

- [@XiangHui](https://github.com/xianghui556)
