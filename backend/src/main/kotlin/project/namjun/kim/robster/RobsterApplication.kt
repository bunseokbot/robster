package project.namjun.kim.robster

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration
import org.springframework.boot.runApplication

@SpringBootApplication(exclude = [SecurityAutoConfiguration::class])
class RobsterApplication

fun main(args: Array<String>) {
    runApplication<RobsterApplication>(*args)
}
