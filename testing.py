from datetime import datetime
from typing import List

from bt4.backend.core.connection.session import Base, DatabaseSessionManager
from sqlalchemy import DateTime, ForeignKey, Integer, String, select
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship


class Order(Base):
    __tablename__ = "Order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("Product.id", ondelete="CASCADE"))
    customer_name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    desc: Mapped[str] = mapped_column(String)


class Product(Base):
    __tablename__ = "Product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = Mapped(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)

    order: Mapped[List[Order]] = relationship("Order", order_by=Order.created_at.desc(), backref="a")


class ProductManagement:

    def register_product(product_name: str):
        db_manager = DatabaseSessionManager.instance()
        db_manager.init_sync()

        with db_manager.session() as session:
            product = Product(product_name=product_name)
            session.add(product)
            session.commit()

        return product

    def buy_product(product_id: int, customer_name: str):
        db_manager = DatabaseSessionManager.instance()
        db_manager.init_sync()

        with db_manager.session() as session:
            order = Order(product_id=product_id, customer_name=customer_name)
            session.add(order)
            session.commit()

        return order

    def load_product_Order(product_id: int):
        db_manager = DatabaseSessionManager.instance()
        db_manager.init_sync()

        with db_manager.session() as session:
            stmt = select(Product).where(Product.id == product_id).options(joinedload(Product.order))
            product = session.execute(stmt)
            product = product.scalar()

        # 검색이 실패하는경우, 특정 아이디를 넣었는데 원하는 값이 없는 경우 product는 None이 리턴된다.
        # None이 리턴되면 product.order에 접근이 불가능해서 오류가 생긴다.
        for i in product.order:
            print(i)

        try:
            for i in product.order:
                print(i)
        except:
            print("해당 제품을 찾을 수 없습니다.")
