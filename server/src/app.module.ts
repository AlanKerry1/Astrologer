import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { VeshunModule } from './veshun/veshun.module';
import { OpenaiService } from './veshun/openai/openai.service';
import { OpenaiModule } from './veshun/openai/openai.module';
import { ConfigModule } from '@nestjs/config';

@Module({
  controllers: [AppController],
  imports: [VeshunModule],
  providers: [],
})
export class AppModule {}
