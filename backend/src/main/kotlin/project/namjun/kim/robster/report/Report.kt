package project.namjun.kim.robster.report

import org.springframework.data.mongodb.core.mapping.Document
import org.springframework.data.mongodb.core.mapping.Field

@Document(collection="reports")
data class Report(
    @Field("_id")
    var id: String,

    @Field("time")
    var time: String,

    @Field("models")
    var models: List<Model>,

    @Field("keywords")
    var keywords: List<Keyword>,

    @Field("methods")
    var methods: List<Method>
)

data class Node(
    var name: String,
    var index: Int = 0
)

data class Model(
    var type: String,
    var path: String,
    var hash: String,
    var structure: List<Node>
)

data class Keyword(
    var keyword: String,
    var path: String
)

data class Method(
    var type: String,
    var method: String
)
