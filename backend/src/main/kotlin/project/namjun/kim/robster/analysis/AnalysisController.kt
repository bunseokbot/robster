package project.namjun.kim.robster.analysis

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import project.namjun.kim.robster.proto.RobsterGrpc
import project.namjun.kim.robster.proto.RobsterOuterClass

@RestController
@RequestMapping("/analysis")
class AnalysisController {

    @Autowired
    lateinit var analysisService: AnalysisService

    @GetMapping("/test")
    fun testMethod(): String {
        return analysisService.executeAnalysis()
    }

}