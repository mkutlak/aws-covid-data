TARGETS=all clean
SUBDIR=src

${TARGETS}: ${SUBDIR}
$(SUBDIR):
	$(MAKE) -C $@ $(MAKECMDGOALS)
.PHONY: ${TARGETS} ${SUBDIR}

all: validate
.PHONY: all

init:
	@echo "Initializing Terraform."
	@terraform init

validate:
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
