-- 修复 daily_news 表：添加 date 列
ALTER TABLE daily_news ADD COLUMN date TEXT;
UPDATE daily_news SET date = datetime(created_at) WHERE date IS NULL;
