package project.namjun.kim.robster.report

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/report")
class ReportController {
    @GetMapping("/{reportId}")
    fun getReportById(@PathVariable("reportId") reportId: String): String {
        return "test"
    }
}