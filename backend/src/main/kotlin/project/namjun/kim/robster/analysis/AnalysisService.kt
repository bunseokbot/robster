package project.namjun.kim.robster.analysis

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import project.namjun.kim.robster.proto.RobsterGrpc
import project.namjun.kim.robster.proto.RobsterOuterClass
import java.util.*

@Service
class AnalysisService {
    @Value("\${robster.analyzer.host}")
    lateinit var analyzerHost: String

    @Value("\${robster.analyzer.port}")
    var analyzerPort: Int = 0
    val uniqueId: String = UUID.randomUUID().toString()

    fun executeAnalysis(analysisDTO: AnalysisDTO): RobsterOuterClass.AnalysisResponse {
        var managedChannel: ManagedChannel = ManagedChannelBuilder.forAddress(
            analyzerHost, analyzerPort
        ).usePlaintext().build()
        var robsterStub: RobsterGrpc.RobsterBlockingStub = RobsterGrpc.newBlockingStub(managedChannel)
        var analysisRequest: RobsterOuterClass.AnalysisRequest = RobsterOuterClass.AnalysisRequest.newBuilder()
            .setId(uniqueId)
            .setPath(analysisDTO.requestPath)
            .setType(analysisDTO.requestType)
            .build()

        var analysisResponse: RobsterOuterClass.AnalysisResponse = robsterStub.executeAnalysis(analysisRequest)
        managedChannel.shutdown()
        return analysisResponse
    }
}