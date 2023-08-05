# vaml: Azure DevOps Variable Groups as YAML files

vaml helps you get Azure DevOps variable groups as simple YAML files,
making it easier than the current UI to modify a large amount of variable groups,
while also allowing to put them back into the AZDO Library.

## Introduction

`vaml` is a tool to get and put Azure DevOps variable groups as files in YAML format.

## Why?

When you have multiple variable group to modify, the Azure DevOps interface can be a nuescence,
going back and forth between variable groups while searching means you have to search again, and again,
and again, this is very time consuming.

So I wanted a tool to obtain one, many or all variable groups in a project in one sweep, modify them locally,
and them put them back.

## Usage

VAML requires 3 things:
- Organization
- Project
- Personal Access Token (Please create this in Azure DevOps)

They can be set as environment variables:
- VAML_ORGANIZATION
- VAML_PROJECT
- VAML_PAT

Example:
```
export VAML_ORGANIZATION=ExampleOrg
export VAML_PROJECT=ExampleProject
export VAML_PAT=accesstokengoeshere
vaml get 'project-testing*'
```

As a config file in (~/.vaml.cfg)
```
organization: ExampleOrg
project: ExampleProject
pat: accesstokengoeshere
```

Example: `vaml get 'project-testing*'`

Or as arguments:
`./vaml --organization ExampleOrg --project ExampleProject -pat accesstokengoeshere get 'testing-project*'` to get the arguments per command.

Currently supported commands:
- get
- put

## Caveats

Currently only GET and PUT operations are allowed, so there's the following Todo

## Todo

- Create and delete operations
- Ability to identify mixed operations, update and create for one-off operations
