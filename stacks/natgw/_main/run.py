"""
# Copyright (C) 2025 Gary Leong <gary@config0.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from config0_publisher.terraform import TFConstructor


def run(stackargs):

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name",
                             tags="tfvar,db",
                             types="str")

    stack.parse.add_optional(key="tier_level",
                             types="str,int")

    # vpc_id is only used for "selectors"
    # e.g. you need to create the vpc before getting the id unless
    # using a selector to query the value after creation
    stack.parse.add_optional(key="vpc_id",
                             types="str",
                             default="null")

    # if eks_cluster is specified, then add the correct tags to the vpc
    stack.parse.add_optional(key="eks_cluster",
                             types="str")

    # docker image to execute terraform with
    stack.parse.add_optional(key="aws_default_region",
                             default="eu-west-1",
                             tags="tfvar,db,resource,tf_exec_env",
                             types="str")

    # Add execgroup
    #stack.add_execgroup("williaumwu:::config0-test1::vpc_simple")

    ## Add substack
    #stack.add_substack('williaumwu:::tf_executor')

    # Initialize
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    return stack.get_results()


