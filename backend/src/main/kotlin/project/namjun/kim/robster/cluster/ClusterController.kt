package project.namjun.kim.robster.cluster

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.data.mongodb.core.MongoTemplate
import org.springframework.data.mongodb.core.find
import org.springframework.data.mongodb.core.query.Criteria
import org.springframework.data.mongodb.core.query.Query
import org.springframework.data.mongodb.core.query.isEqualTo
import org.springframework.web.bind.annotation.*
import project.namjun.kim.robster.report.Report

@RestController
@RequestMapping("/cluster")
class ClusterController {

    @Autowired
    private lateinit var mongoTemplate: MongoTemplate

    @GetMapping("/model/hash/{modelHash}")
    fun clusterModelByHash(@PathVariable("modelHash") modelHash: String): List<Cluster>? {
        val query: Query = Query()
            .addCriteria(
                Criteria.where("models").elemMatch(
                    Criteria.where("hash").isEqualTo(modelHash)
                )
            )
        query.fields().include("_id", "time")

        return this.mongoTemplate.find(query, "reports")
    }

    @GetMapping("/model/type/{modelType}")
    fun clusterModelByType(@PathVariable("modelType") modelType: String): List<Cluster>? {
        val query: Query = Query()
            .addCriteria(
                Criteria.where("models").elemMatch(
                    Criteria.where("type").isEqualTo(modelType)
                )
            )

        return this.mongoTemplate.find(query, "reports")
    }

    @GetMapping("/method/type/{methodType}")
    fun clusterMethodByType(@PathVariable("methodType") methodType: String): List<Cluster>? {
        val query: Query = Query()
            .addCriteria(
                Criteria.where("methods").elemMatch(
                    Criteria.where("type").isEqualTo(methodType)
                )
            )

        return this.mongoTemplate.find(query, "reports")
    }
}