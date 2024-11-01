INSERT INTO "PEOPLE_CHARACTER" ("People_ID", "Character") VALUES
(1, '細心'),
(1, '有條理'),
(2, '友善'),
(2, '細心'),
(2, '有條理'),
(3, '有條理'),
(4, '活潑'),
(4, '善於社交'),
(5, '樂觀'),
(5, '有條理'),
(6, '喜歡冒險'),
(6, '活潑'),
(7, '務實'),
(8, '務實'),
(9, '活潑'),
(9, '喜歡冒險'),
(10, '善於社交'),
(10, '友善');

INSERT INTO "HOUSE_FURNITURE" ("House_ID", "Furniture") VALUES
(1, '衣櫃'),
(1, '茶几'),
(1, '床'),
(2, '床'),
(2, '書桌'),
(3, '書架'),
(3, '書桌'),
(4, '書架'),
(4, '書桌'),
(4, '床'),
(5, '衣櫃'),
(5, '床');

INSERT INTO "HOUSE_TRAFFIC" ("House_ID", "Traffic")
VALUES
(1, '捷運'),
(2, '公車'),
(3, '捷運'),
(4, '公車'),
(5, '捷運');

INSERT INTO "PREFERENCE" ("Preference_ID", "People_ID")
VALUES
(1, 2),
(2, 4),
(3, 6),
(4, 8),
(5, 10);

INSERT INTO "PREFERENCE_HOUSE_PLACE" ("Preference_ID", "Preference_House_Place")
VALUES
(1, '大安區'),
(1, '文山區'),
(2, '大安區'),
(2, '文山區'),
(3, '新店區'),
(4, '士林區'),
(4, '北投區'),
(5, '新店區');
