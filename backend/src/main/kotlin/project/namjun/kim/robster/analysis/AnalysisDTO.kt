package project.namjun.kim.robster.analysis

import com.fasterxml.jackson.annotation.JsonProperty

data class AnalysisDTO(
    @JsonProperty("path")
    var requestPath: String,

    @JsonProperty("type")
    var requestType: String
)
