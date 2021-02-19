package project.namjun.kim.robster.analysis

import org.springframework.beans.factory.annotation.Value
import org.springframework.core.io.Resource
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.io.InputStream
import java.nio.file.FileAlreadyExistsException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.security.MessageDigest

@Service
class FileStorageImpl: FileStorage {
    @Value("\${robster.storage}")
    lateinit var storage: String

    override fun storeFile(file: MultipartFile): String {
        val rootLocation: Path = Paths.get(this.storage)
        val filename: String = calculateHash(file.inputStream)
        try {
            Files.copy(file.inputStream, rootLocation.resolve(filename))
        } catch (e: FileAlreadyExistsException) {

        }
        return Paths.get(this.storage, filename).toString()
    }

    override fun loadFile(path: String): Resource {
        TODO("Not yet implemented")
    }

    override fun getFileHash(path: String): String {
        TODO("Not yet implemented")
    }

    fun calculateHash(stream: InputStream): String {
        return MessageDigest
            .getInstance("SHA-256")
            .digest(stream.readAllBytes())
            .fold("", { str, it -> str + "%02x".format(it) })
    }
}