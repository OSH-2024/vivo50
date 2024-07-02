#include<cstdio>
#include<iostream>
#include<cstring>
#include<algorithm>
#define re register
#define int long long
#define maxn 100010
#define ls p<<1
#define rs p<<1|1
#define size (r-l+1)

using namespace std;

inline int read()
{
	int x=0,f=1; char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-'0';ch=getchar();}
	return x*f;
}
int ans;
int n,m,sums[maxn<<2],lazy[maxn<<2],opt,x,y,k,a[maxn];
void push_up(int p)
{
	sums[p]=sums[ls]+sums[rs];
}
void push_down(int p,int l,int r)
{
	int mid=(l+r)>>1;
	lazy[ls]+=lazy[p];
	lazy[rs]+=lazy[p];
	sums[ls]+=(mid-l+1)*lazy[p];
	sums[rs]+=(r-mid)*lazy[p];
	lazy[p]=0;
}
void build(int l,int r,int p)
{
	if(l==r)
	{
		sums[p]=a[l];
		return ;
	}
	int mid=(l+r)>>1;
	build(l,mid,ls);
	build(mid+1,r,rs);
	push_up(p); 
}
void modify(int l,int r,int ql,int qr,int v,int p)
{
	if(ql<=l&&r<=qr)
	{
		sums[p]+=size*v;
		lazy[p]+=v;
		return;
	}
	push_down(p,l,r);
	int mid=(l+r)>>1;
	if(ql<=mid) modify(l,mid,ql,qr,v,ls);
	if(qr>mid) modify(mid+1,r,ql,qr,v,rs);
	push_up(p);
}
void query(int l,int r,int ql,int qr,int p)
{
	if(ql<=l&&r<=qr)
	{
		ans+=sums[p];
		return; 
	}
	push_down(p,l,r);
	int mid=(l+r)>>1;
	if(ql<=mid) query(l,mid,ql,qr,ls);
	if(qr>mid) query(mid+1,r,ql,qr,rs);
}
signed main()
{
//	freopen("1.in","r",stdin);
	n=read(),m=read();
	for(re int i=1;i<=n;++i) a[i]=read();
	build(1,n,1);
	for(re int i=1;i<=m;++i)
	{
		opt=read();
		if(opt==1)
		{
			x=read(),y=read(),k=read();
			modify(1,n,x,y,k,1);
		}
		else
		{
			x=read(),y=read();
			ans=0;
			query(1,n,x,y,1);
			printf("%lld\n",ans);
		}
	}
	return 0;
}