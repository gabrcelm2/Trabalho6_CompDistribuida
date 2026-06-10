package br.unifor.streaming_musicas.config;

import br.unifor.streaming_musicas.grpc.StreamingGrpcService;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import java.io.IOException;

@Component
public class GrpcServerRunner {

    private final StreamingGrpcService streamingGrpcService;
    private Server server;

    public GrpcServerRunner(StreamingGrpcService streamingGrpcService) {
        this.streamingGrpcService = streamingGrpcService;
    }

    @PostConstruct
    public void start() throws IOException {
        server = ServerBuilder.forPort(9090)
                .addService(streamingGrpcService)
                .build()
                .start();
        System.out.println("gRPC Server started on port 9090");
    }

    @PreDestroy
    public void stop() {
        if (server != null) {
            server.shutdown();
        }
    }
}
