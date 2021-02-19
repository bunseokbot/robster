package project.namjun.kim.robster.report

import org.springframework.data.mongodb.repository.MongoRepository
import org.springframework.stereotype.Repository

@Repository
interface ReportRepository: MongoRepository<Report, String> {
    fun getReportById(reportId: String): Report
}
