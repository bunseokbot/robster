package project.namjun.kim.robster.analysis

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.*
import project.namjun.kim.robster.proto.RobsterGrpc
import project.namjun.kim.robster.proto.RobsterOuterClass

@RestController
@RequestMapping("/analysis")
class AnalysisController {

    @Autowired
    lateinit var analysisService: AnalysisService

    @PostMapping("/")
    fun requestAnalysis(@RequestBody analysisDTO: AnalysisDTO): AnalysisMapping {
        var analysisResult: RobsterOuterClass.AnalysisResponse = analysisService.executeAnalysis(analysisDTO)
        return AnalysisMapping(
            id = analysisResult.id,
            status = analysisResult.status,
            message = analysisResult.message
        )
    }

}