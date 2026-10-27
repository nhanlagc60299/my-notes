# Câu truyền cảm hứng — học tech, AI, design & system thinking

Email flashcard hằng ngày lấy **1 câu** trong file này (xoay vòng theo ngày) và đặt ở đầu email.

**Quy tắc:** chỉ thêm câu **truy được nguồn gốc** (sách, bài báo, bài giảng, email lưu trữ), không lấy từ trang tổng hợp quote. Nhiều câu "nổi tiếng" thực ra bị gán nhầm (vd: "If you can't measure it, you can't manage it" không phải của Drucker; "Tell me and I forget…" không phải của Franklin), nên không dùng. Nguồn gốc đã kiểm chứng ghi ✅; chỉ có nguồn thứ cấp nhất quán thì ghi ⚠️.

**Quy ước** (để script đọc được): heading `### Q-NN · <Nhóm>`, sau đó là dòng `> "<câu gốc>"` và các trường `**Dịch:**`, `**Tác giả:**`, `**Ý cho mình:**`, `**Nguồn:**`.

---

### Q-01 · Học tập
> "What I cannot create, I do not understand."
**Dịch:** Cái gì tôi không tự làm ra được thì tôi chưa hiểu nó.
**Tác giả:** Richard Feynman, câu viết trên bảng đen lúc ông mất (1988)
**Ý cho mình:** Đọc note chưa đủ. Phải tự gõ lại agent loop thì mới biết mình hiểu tới đâu.
**Nguồn:** Ảnh bảng đen trong Caltech Archives, được Scientific American và 3 Quarks Daily trích lại · ✅

### Q-02 · AI
> "We can only see a short distance ahead, but we can see plenty there that needs to be done."
**Dịch:** Ta chỉ nhìn được một quãng ngắn phía trước, nhưng trong quãng đó đã có rất nhiều việc cần làm.
**Tác giả:** Alan Turing, "Computing Machinery and Intelligence", *Mind* 59 (1950)
**Ý cho mình:** Không cần biết AI 5 năm nữa ra sao mới bắt đầu. Buổi kế đã có đủ việc để làm.
**Nguồn:** Câu cuối bài báo, *Mind* 59(236): 433–460 · ✅

### Q-03 · Học tập
> "The best way to predict the future is to invent it."
**Dịch:** Cách tốt nhất để dự đoán tương lai là tự tạo ra nó.
**Tác giả:** Alan Kay (1971, cuộc họp với Xerox PARC)
**Ý cho mình:** Thay vì đọc thêm một bài "AI agent sẽ thay đổi SRE", hãy tự làm một agent chạy được.
**Nguồn:** Quote Investigator truy về Alan Kay năm 1971 · ✅

### Q-04 · Design
> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
**Dịch:** Ai cũng viết được code mà máy hiểu. Lập trình viên giỏi viết code mà người khác hiểu được.
**Tác giả:** Martin Fowler, *Refactoring* (1999)
**Ý cho mình:** Prompt cũng là code. Người on-call lúc 3 giờ sáng cần đọc được prompt và tool description.
**Nguồn:** Martin Fowler, *Refactoring: Improving the Design of Existing Code*, Addison-Wesley, 1999 · ✅

### Q-05 · Học tập
> "Talk is cheap. Show me the code."
**Dịch:** Nói thì dễ. Đưa code ra xem.
**Tác giả:** Linus Torvalds, email trên Linux Kernel Mailing List (25/08/2000)
**Ý cho mình:** Mỗi buổi học kết thúc bằng `pytest -q` xanh, không phải bằng cảm giác "mình hiểu rồi".
**Nguồn:** Computer History Museum và Wikiquote trích email LKML ngày 2000-08-25; chưa mở được bản lưu trữ gốc · ⚠️ một phần

### Q-06 · Vận hành
> "Hope is not a strategy."
**Dịch:** Hy vọng không phải là chiến lược.
**Tác giả:** Câu nói truyền thống của SRE, mở đầu chương 1 của *Site Reliability Engineering* (Google, 2016)
**Ý cho mình:** "Chắc model sẽ trả JSON đúng" là hy vọng. Schema, validate, retry và eval mới là chiến lược.
**Nguồn:** sre.google/sre-book, chương 1 "Introduction" · ✅

### Q-07 · AI
> "Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short."
**Dịch:** Bắt đầu bằng prompt đơn giản, tối ưu bằng đánh giá (eval) đầy đủ, và chỉ thêm hệ thống agent nhiều bước khi cách đơn giản không đủ.
**Tác giả:** Anthropic, "Building effective agents" (12/2024)
**Ý cho mình:** Agent không phải mặc định. Một lời gọi LLM với eval tốt thường đã đủ.
**Nguồn:** anthropic.com/engineering/building-effective-agents, phần Summary · ✅

### Q-08 · Design
> "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. The first method is far more difficult."
**Dịch:** Có hai cách thiết kế phần mềm: làm nó đơn giản tới mức hiển nhiên không có lỗi, hoặc làm nó phức tạp tới mức không có lỗi nào hiển nhiên. Cách thứ nhất khó hơn nhiều.
**Tác giả:** C. A. R. (Tony) Hoare, bài giảng Turing Award "The Emperor's Old Clothes" (1980)
**Ý cho mình:** Graph agent càng nhiều node thì lỗi càng khó thấy. Thiết kế sao cho đọc vào là thấy được nó đúng.
**Nguồn:** *Communications of the ACM* 24(2): 75–83, tháng 2/1981 · ✅

### Q-09 · System thinking
> "A complex system that works is invariably found to have evolved from a simple system that worked."
**Dịch:** Một hệ phức tạp chạy được luôn là kết quả tiến hoá từ một hệ đơn giản đã chạy được.
**Tác giả:** John Gall, *Systemantics* (1975), gọi là "Gall's Law"
**Ý cho mình:** Đây là lý do lộ trình bắt đầu bằng `01_hello_brain.py` một lời gọi model, rồi mới thêm tool, memory, guardrail.
**Nguồn:** John Gall, *Systemantics: How Systems Work and Especially How They Fail*, 1975; câu chữ khớp nhau ở nhiều nguồn thứ cấp, chưa xem bản gốc · ⚠️ một phần

### Q-10 · System thinking
> "Organizations which design systems … are constrained to produce designs which are copies of the communication structures of these organizations."
**Dịch:** Tổ chức thiết kế hệ thống sẽ bị ràng buộc phải tạo ra thiết kế sao chép cấu trúc giao tiếp của chính tổ chức đó.
**Tác giả:** Melvin Conway, "How Do Committees Invent?" (1968), gọi là "Conway's Law"
**Ý cho mình:** Multi-agent cũng vậy: cách chia agent và cách chúng "nói chuyện" sẽ quyết định kiến trúc, kể cả chỗ hỏng.
**Nguồn:** *Datamation* 14(4): 28–31, tháng 4/1968; tóm tắt của Adrian Colyer (ACM Queue, The Morning Paper) · ✅

### Q-11 · System thinking
> "A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable."
**Dịch:** Hệ phân tán là hệ mà một máy tính bạn còn không biết là có tồn tại lại có thể làm máy của bạn không dùng được.
**Tác giả:** Leslie Lamport, email gửi bảng tin DEC SRC (28/05/1987)
**Ý cho mình:** Agent gọi model, MCP server và vector DB đã là một hệ phân tán. Cần timeout, retry và circuit breaker từ đầu.
**Nguồn:** Microsoft Research (trang của Lamport) lưu nguyên văn email ngày 1987-05-28 · ✅

### Q-12 · Vận hành
> "Complex systems run as broken systems."
**Dịch:** Hệ phức tạp luôn vận hành trong trạng thái đang hỏng một phần.
**Tác giả:** Richard I. Cook, "How Complex Systems Fail" (1998)
**Ý cho mình:** Agent luôn có lỗi mềm (sai nhãn, retrieve sai). Câu hỏi đúng là lỗi đó có bị đo, bị chặn trước khi gây hại không.
**Nguồn:** Richard I. Cook, *How Complex Systems Fail*, Cognitive Technologies Laboratory, University of Chicago, 1998–2000, điểm 5 "Complex systems run in degraded mode" · ✅
