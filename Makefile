TARGETS=all clean
SUBDIR=src
TERRAFORM=.terraform

${TARGETS}: ${SUBDIR}
$(SUBDIR):
	$(MAKE) -C $@ $(MAKECMDGOALS)
.PHONY: ${TARGETS} ${SUBDIR}

all: validate
.PHONY: all

${TERRAFORM}:
	@echo "Initializing Terraform."
	@terraform init

init: ${TERRAFORM}

validate: init
	@echo "Validating Terraform"
	@terraform fmt --check
	@terraform validate

plan: validate
	@echo "Planning Terraform deployment."
	terraform plan

apply: validate
	@echo "Deploying Terraform to AWS."
	terraform apply

destroy: confirm
	@echo "Destroying the AWS deployment."
	terraform destroy

confirm:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} == y ]

clean:
	@echo "Cleaning Terraform deployment."
	rm -rf "./${TERRAFORM}"
