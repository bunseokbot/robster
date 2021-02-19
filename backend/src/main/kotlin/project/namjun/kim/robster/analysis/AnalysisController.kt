package project.namjun.kim.robster.analysis

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile
import project.namjun.kim.robster.proto.RobsterOuterClass
import java.lang.Exception
import java.nio.file.Path
import java.nio.file.Paths

@RestController
@RequestMapping("/analysis")
class AnalysisController {

    @Autowired
    lateinit var analysisService: AnalysisService

    @Autowired
    lateinit var fileStorage: FileStorage

    private val rootLocation: Path = Paths.get("storage")

    @PostMapping("/")
    fun requestAnalysis(@RequestParam("file") file: MultipartFile): AnalysisMapping {
        val filePath: String = fileStorage.storeFile(file)
        val analysisResult: RobsterOuterClass.AnalysisResponse = analysisService.executeAnalysis(
            filePath = filePath,
            fileType = "apk"
        )
        return AnalysisMapping(
            id = analysisResult.id,
            status = analysisResult.status,
            message = analysisResult.message
        )
    }

}