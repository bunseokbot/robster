package project.namjun.kim.robster.report

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.data.mongodb.core.MongoTemplate
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/report")
class ReportController {

    @Autowired
    private lateinit var reportRepository: ReportRepository

    @GetMapping("/{reportId}")
    fun getReportById(@PathVariable("reportId") reportId: String): Report? {
        return reportRepository.getReportById(reportId)
    }

}