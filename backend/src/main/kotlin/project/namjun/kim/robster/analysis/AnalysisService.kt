package project.namjun.kim.robster.analysis

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import project.namjun.kim.robster.proto.RobsterGrpc
import project.namjun.kim.robster.proto.RobsterOuterClass

@Service
class AnalysisService {
    @Value("\${robster.analyzer.host}")
    lateinit var analyzerHost: String

    @Value("\${robster.analyzer.port}")
    var analyzerPort: Int = 0

    fun executeAnalysis(): String {
        var managedChannel: ManagedChannel = ManagedChannelBuilder.forAddress(
            analyzerHost, analyzerPort
        ).usePlaintext().build()
        var robsterStub: RobsterGrpc.RobsterBlockingStub = RobsterGrpc.newBlockingStub(managedChannel)
        var analysisRequest: RobsterOuterClass.AnalysisRequest = RobsterOuterClass.AnalysisRequest.newBuilder()
            .setId("id")
            .setPath("D:\\dev\\ml-attacker\\binaries\\com.hyundaicard.appcard.apk")
            .setType("apk")
            .build()

        var analysisResponse: RobsterOuterClass.AnalysisResponse = robsterStub.executeAnalysis(analysisRequest)
        managedChannel.shutdown()
        return analysisResponse.message
    }
}