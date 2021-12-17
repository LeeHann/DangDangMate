<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ page import="java.io.PrintWriter"%>
<%@ page import="bbs.BbsDAO"%>
<%@ page import="bbs.Bbs"%>
<%@ page import="java.util.ArrayList"%>
<% request.setCharacterEncoding("UTF-8"); %>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width" initial-scale="1">
<link rel="stylesheet" href="css/bootstrap.css">
<title>JSP JSW 게시판 웹사이트</title>
<style type="text/css">
a, a:hover {
	color: #000000;
	text-decoration: none;
}
</style>
</head>
<body>
	<%
		String userID = null;
		if(session.getAttribute("userID") != null) {
			userID = (String) session.getAttribute("userID");
		}
		int pageNumber =1;
		if(request.getParameter("pageNumber")!=null){
			pageNumber = Integer.parseInt(request.getParameter("pageNumber"));
			System.out.println("pageNumber="+pageNumber);
		}
		String searchWord = null;
		if(request.getParameter("searchWord")!=null){
			searchWord = (String) request.getParameter("searchWord");
			System.out.println("searchword from parameter is :" + searchWord);
		}
		if(session.getAttribute("searchWord")!=null){
			searchWord = (String) session.getAttribute("searchWord");
			System.out.println("searchword from session is :" + searchWord);
		}
	%>
	<nav class="navbar navbar-default">
		<div class="navbar-header">
			<button type="button" class="navbar-toggle collapsed"
				data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"
				aria-expanded="false">
				<span class="icon-bar"></span> <span class="icon-bar"></span> <span
					class="icon-bar"></span>
			</button>
			<a class="navbar-brand" href="main.jsp">JSP 게시판 메인</a>
		</div>
		<div class="collapse navbar-collapse"
			id="bs-example-navbar-collapse-1">
			<ui class="nav navbar-nav">
			<li><a href="main.jsp">메인</a></li>
			<li class="active"><a href="bbs.jsp">게시판</a></li>
			</ui>
			<%
			if( userID ==null ) {
		%>
			<ui class="nav navbar-nav navbar-right">
			<li class="dropdown"><a href="#" class="dropdown-toggle"
				data-toggle="dropdown" role="button" aria-haspopup="true"
				aria-expanded="false">접속하기<span class="caret"></</span></a>
				<ul class="dropdown-menu">
					<li class="active"><a href="login.jsp">로그인</a></li>
					<li><a href="join.jsp">회원가입</a></li>
				</ul></li>
			</ui>
			<%	
			} else {
		%>
			<ui class="nav navbar-nav navbar-right">
			<li class="dropdown"><a href="#" class="dropdown-toggle"
				data-toggle="dropdown" role="button" aria-haspopup="true"
				aria-expanded="false">회원관리<span class="caret"></</span></a>
				<ul class="dropdown-menu">
					<li><a href="logoutAction.jsp">로그아웃</a></li>
				</ul></li>
			</ui>
			<% 
			}
		%>
		</div>
	</nav>
	<div class="container">
		<div class="row">
			<table class="table table-striped"
				style="text-align: center; border: 1px solid #dddddd">
				<thead>
					<div>
						<div class=" col-lg-4">
							<input type="text" class="form-control pull-right" placeholder="Search" id="txtSearch" />
						</div>
						<button class="btn btn-primary" type="submit">
							<span class="glyphicon glyphicon-search"></span>
							<a href="searchedBbs.jsp"></a>
						</button>
					</div>
					<tr>
						<th style="background-color: #eeeeee; text-align: center;">번호</th>
						<th style="background-color: #eeeeee; text-align: center;">제목</th>
						<th style="background-color: #eeeeee; text-align: center;">작성자</th>
						<th style="background-color: #eeeeee; text-align: center;">작성일</th>
					</tr>
				</thead>
				<tbody>
					<%
						BbsDAO bbsDAO = new BbsDAO();
						//System.out.println("here before getlist");
						ArrayList<Bbs> list = bbsDAO.getSearchedList(pageNumber,searchWord);
						//System.out.println("here after getlist" + list.get(0).getBbsDate().substring(0,11));
						for(int i=0;i<list.size();i++){
					%>
					<tr>
						<td><%=list.get(i).getBbsID()%></td>
						<td><a href="view.jsp?bbsID=<%=list.get(i).getBbsID()%>"><%=list.get(i).getBbsTitle().replaceAll(" ","&nbsp;").replaceAll("<","&lt;").replaceAll("<","&gt;").replaceAll("\n","<br>")%></a></td>
						<td><%= list.get(i).getUserID()%></td>
						<td><%=	list.get(i).getBbsDate().substring(0, 11) + list.get(i).getBbsDate().substring(11,13) + "시" + list.get(i).getBbsDate().substring(14,16) + "분"%></td>
					</tr>
					<% 
					
						}
					
					%>

				</tbody>
			</table>

				<tr>
				
					<td class = "pull-left">
					
					
					
						<% 
				if(pageNumber != 1) {
					session.setAttribute("searchWord",searchWord);
			%> <a href="searchedBbs.jsp?pageNumber=<%=pageNumber-1%>"
						class="btn btn-success btn-arrow-left">이전</a> <%		
				} if(bbsDAO.searchedNextPage(pageNumber,searchWord)) {
					session.setAttribute("searchWord",searchWord);
			%> <a href="searchedBbs.jsp?pageNumber=<%=pageNumber+1%>"
						class="btn btn-success btn-arrow-right">다음</a> <% 
				}
			%>
					</td>
					
					<td><a href="write.jsp" class="btn btn-primary pull-right">글쓰기</a>
					</td>
				</tr>

			
		</div>
	</div>
	<script src="http://code.jquery.com/jquery-3.1.1.min.js"></script>
	<script src="js/bootstrap.js"></script>
</body>
</html>