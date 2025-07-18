import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AstrologerModule } from './astrologer/astrologer.module';
import { OpenaiService } from './astrologer/openai/openai.service';
import { OpenaiModule } from './astrologer/openai/openai.module';
import { ConfigModule } from '@nestjs/config';

@Module({
  controllers: [AppController],
  imports: [AstrologerModule],
  providers: [],
})
export class AppModule {}
