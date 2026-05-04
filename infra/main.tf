terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource group for the entire project
resource "azurerm_resource_group" "rg" {
  name     = "multi-agent-lab-rg"
  location = "eastus"
}

# VM module (we will create vm.tf next)
module "vm" {
  source = "./vm"
}
