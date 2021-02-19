package project.namjun.kim.robster.analysis

import org.springframework.core.io.Resource
import org.springframework.web.multipart.MultipartFile

interface FileStorage {
    fun storeFile(file: MultipartFile): String
    fun loadFile(path: String): Resource
    fun getFileHash(path: String): String
}