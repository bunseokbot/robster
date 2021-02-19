package project.namjun.kim.robster.cluster

import org.springframework.data.mongodb.core.mapping.Field

data class Cluster (
    @Field("_id")
    var id: String,

    @Field("time")
    var time: String
)