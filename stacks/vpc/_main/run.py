from config0_publisher.terraform import TFConstructor


def run(stackargs):

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name",
                             tags="tfvar,db",
                             types="str")

    stack.parse.add_optional(key="aws_default_region",
                             default="eu-west-1",
                             tags="tfvar,db,resource,tf_exec_env",
                             types="str")

    # Add execgroup
    stack.add_execgroup("williaumwu::config0-test2::vpc", "tf_execgroup")

    # Add substack - this is default for executing Terraform on Config0
    # but users can create their own implementation
    stack.add_substack('config0-publish:::tf_executor')

    # Initialize
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    # set variables
    _default_tags = {"vpc_name": stack.vpc_name}

    vpc_tags = _default_tags.copy()
    public_subnet_tags = _default_tags.copy()
    private_subnet_tags = _default_tags.copy()

    # if eks_cluster is provided, we modify the configs
    # if we are using a vpc without a nat, the eks must be in public network
    # the internal lb must also be in public
    if stack.get_attr("eks_cluster"):
        vpc_tags[f"kubernetes.io/cluster/{stack.eks_cluster}"] = "shared"
        public_subnet_tags["kubernetes.io/role/elb"] = "1"
        private_subnet_tags["kubernetes.io/role/internal_elb"] = "1"

    stack.set_variable("vpc_tags",
                       vpc_tags,
                       tags="tfvar",
                       types="dict")

    stack.set_variable("public_subnet_tags", 
                       public_subnet_tags,
                       tags="tfvar",
                       types="dict")

    stack.set_variable("private_subnet_tags", 
                       private_subnet_tags,
                       tags="tfvar",
                       types="dict")

    stack.set_variable("timeout", 600)

    # use the terraform constructor (helper)
    tf = TFConstructor(stack=stack,
                       execgroup_name=stack.tf_execgroup.name,
                       provider="aws",
                       tf_runtime="tofu:1.9.1",
                       resource_name=stack.vpc_name,
                       resource_type="vpc")

    # values to include to root level of the config0 db to query
    tf.include(values={
        "aws_default_region": stack.aws_default_region,
        "name": stack.vpc_name,
        "vpc": stack.vpc_name,
        "vpc_name": stack.vpc_name
    })

    # publish the info
    tf.output(keys=["aws_default_region",
                    "vpc_name",
                    "vpc_id"])

    # finalize the tf_executor
    stack.tf_executor.insert(display=True,
                             **tf.get())

    return stack.get_results()
