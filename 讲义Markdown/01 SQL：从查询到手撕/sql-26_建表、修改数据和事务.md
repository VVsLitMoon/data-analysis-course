# sql-26 · 建表、修改数据和事务

## 查询之外还有什么
CREATE TABLE 定义列与类型，INSERT 添加行，UPDATE 修改行，DELETE 删除行，DROP TABLE 删除整表。读题阶段通常只需要 SELECT，真实工作中修改数据应先确认范围和备份。
## 约束防止坏数据
PRIMARY KEY 唯一且非空；UNIQUE 通常限制重复；NOT NULL 不许缺失；CHECK 表达取值规则；FOREIGN KEY 约束关联。数据库约束和业务校验互相补充。
## 事务把操作当作一组
START TRANSACTION 开始，COMMIT 确认，ROLLBACK 撤销未提交修改。下面只改讲义的 scratch 表，回滚后恢复。InnoDB 支持事务，DDL 常有隐式提交，不能假设 DROP 可回滚。
ACID 分别是原子性、一致性、隔离性、持久性。脏读、不可重复读、幻读是并发观察问题；隔离级别与 MVCC、锁的细节放在面试进阶。

## 可运行例子

```sql
SELECT *
FROM scratch;
START TRANSACTION;
UPDATE scratch SET amount=99
WHERE id=1;
SELECT *
FROM scratch;
ROLLBACK;
SELECT *
FROM scratch;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

ROLLBACK 在这里的作用是？

1. 按金额排序
2. 撤销未提交修改
3. 永久删除数据库

<details><summary>答案与解释</summary>

答案：2。本例只涉及支持事务的表内 DML。

</details>
